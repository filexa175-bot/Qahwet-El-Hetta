const { onUserCreated } = require("firebase-functions/v2/identity");
const { onCall, HttpsError } = require("firebase-functions/v2/https");
const { initializeApp } = require("firebase-admin/app");
const { getFirestore, FieldValue } = require("firebase-admin/firestore");

initializeApp();
const db = getFirestore();

// Cairo calendar day, independent of the device clock/time zone.
function cairoDay() {
  return new Intl.DateTimeFormat("en-CA", {
    timeZone: "Africa/Cairo", year: "numeric", month: "2-digit", day: "2-digit"
  }).format(new Date());
}

// Registration reward is created exactly once by the trusted Auth trigger.
exports.initializePlayerWallet = onUserCreated(async (event) => {
  const uid = event.data.uid;
  const walletRef = db.doc(`wallets/${uid}`);
  await db.runTransaction(async (tx) => {
    const snap = await tx.get(walletRef);
    if (snap.exists) return;
    tx.create(walletRef, {
      uid,
      balance: 500,
      totalEarned: 500,
      registrationGiftClaimed: true,
      lastDailyGiftDay: null,
      createdAt: FieldValue.serverTimestamp(),
      updatedAt: FieldValue.serverTimestamp()
    });
    tx.create(walletRef.collection("ledger").doc("registration-gift"), {
      type: "registration_gift",
      amount: 500,
      createdAt: FieldValue.serverTimestamp()
    });
  });
});

exports.claimDailyGift = onCall(async (request) => {
  if (!request.auth) throw new HttpsError("unauthenticated", "سجل دخولك أولاً");
  const uid = request.auth.uid;
  const today = cairoDay();
  const walletRef = db.doc(`wallets/${uid}`);
  return db.runTransaction(async (tx) => {
    const snap = await tx.get(walletRef);
    if (!snap.exists) throw new HttpsError("failed-precondition", "محفظة اللاعب غير مهيأة");
    const wallet = snap.data();
    if (wallet.lastDailyGiftDay === today) {
      return { claimed: false, balance: wallet.balance, day: today };
    }
    const balance = Number(wallet.balance || 0) + 500;
    tx.update(walletRef, {
      balance,
      totalEarned: Number(wallet.totalEarned || 0) + 500,
      lastDailyGiftDay: today,
      updatedAt: FieldValue.serverTimestamp()
    });
    tx.create(walletRef.collection("ledger").doc(`daily-${today}`), {
      type: "daily_gift", amount: 500, day: today,
      createdAt: FieldValue.serverTimestamp()
    });
    return { claimed: true, balance, day: today };
  });
});

exports.getWallet = onCall(async (request) => {
  if (!request.auth) throw new HttpsError("unauthenticated", "سجل دخولك أولاً");
  const uid = request.auth.uid;
  const walletRef = db.doc(`wallets/${uid}`);
  // Also initialize accounts created before wallet functions were introduced.
  const data = await db.runTransaction(async (tx) => {
    const snap = await tx.get(walletRef);
    if (snap.exists) return snap.data();
    const initial = {
      uid, balance: 500, totalEarned: 500,
      registrationGiftClaimed: true, lastDailyGiftDay: null,
      createdAt: FieldValue.serverTimestamp(),
      updatedAt: FieldValue.serverTimestamp()
    };
    tx.create(walletRef, initial);
    tx.create(walletRef.collection("ledger").doc("registration-gift"), {
      type: "registration_gift", amount: 500,
      createdAt: FieldValue.serverTimestamp()
    });
    return initial;
  });
  return { balance: Number(data.balance || 0), lastDailyGiftDay: data.lastDailyGiftDay || null, today: cairoDay() };
});


// Accept a friend request atomically and enforce the 15-friend cap for BOTH players.
// Per-player counters serialize concurrent acceptances; Admin SDK bypasses client rules.
exports.respondFriendRequest = onCall(async (request) => {
  if (!request.auth) throw new HttpsError("unauthenticated", "سجل دخولك أولاً");
  const uid = request.auth.uid;
  const requestId = String(request.data?.requestId || "");
  const accept = request.data?.accept === true;
  if (!requestId || requestId.length > 160) {
    throw new HttpsError("invalid-argument", "طلب الصداقة غير صالح");
  }
  const requestRef = db.doc(`friendRequests/${requestId}`);
  const requestSnap = await requestRef.get();
  if (!requestSnap.exists || requestSnap.data().toUid !== uid || requestSnap.data().status !== "pending") {
    throw new HttpsError("failed-precondition", "طلب الصداقة غير متاح");
  }
  const friendRequest = requestSnap.data();
  if (!accept) {
    await requestRef.update({ status: "declined", respondedAt: FieldValue.serverTimestamp() });
    return { accepted: false };
  }

  const fromUid = friendRequest.fromUid;
  const toUid = friendRequest.toUid;
  if (!fromUid || !toUid || fromUid === toUid || toUid !== uid) {
    throw new HttpsError("failed-precondition", "بيانات طلب الصداقة غير صحيحة");
  }
  const fromCountRef = db.doc(`friendCounts/${fromUid}`);
  const toCountRef = db.doc(`friendCounts/${toUid}`);

  // Bootstrap counters for accounts that may already have friendships from an earlier build.
  const [fromExisting, toExisting] = await Promise.all([
    db.collection("friends").where("ownerUid", "==", fromUid).count().get(),
    db.collection("friends").where("ownerUid", "==", toUid).count().get()
  ]);
  const initialCounts = { [fromUid]: fromExisting.data().count, [toUid]: toExisting.data().count };

  return db.runTransaction(async (tx) => {
    const [reqSnap, fromCountSnap, toCountSnap] = await Promise.all([
      tx.get(requestRef), tx.get(fromCountRef), tx.get(toCountRef)
    ]);
    if (!reqSnap.exists || reqSnap.data().toUid !== uid || reqSnap.data().status !== "pending") {
      throw new HttpsError("failed-precondition", "طلب الصداقة لم يعد متاحًا");
    }
    const fromCount = fromCountSnap.exists ? Number(fromCountSnap.data().count || 0) : Number(initialCounts[fromUid] || 0);
    const toCount = toCountSnap.exists ? Number(toCountSnap.data().count || 0) : Number(initialCounts[toUid] || 0);
    if (fromCount >= 15 || toCount >= 15) {
      throw new HttpsError("resource-exhausted", "وصل أحد اللاعبين إلى الحد الأقصى: 15 صديقًا");
    }

    tx.update(requestRef, { status: "accepted", respondedAt: FieldValue.serverTimestamp() });
    tx.set(db.doc(`friends/${fromUid}__${toUid}`), {
      ownerUid: fromUid, friendUid: toUid, friendPlayerId: friendRequest.toPlayerId || "", createdAt: FieldValue.serverTimestamp()
    });
    tx.set(db.doc(`friends/${toUid}__${fromUid}`), {
      ownerUid: toUid, friendUid: fromUid, friendPlayerId: friendRequest.fromPlayerId || "", createdAt: FieldValue.serverTimestamp()
    });
    tx.set(fromCountRef, { uid: fromUid, count: fromCount + 1, updatedAt: FieldValue.serverTimestamp() });
    tx.set(toCountRef, { uid: toUid, count: toCount + 1, updatedAt: FieldValue.serverTimestamp() });
    return { accepted: true, fromCount: fromCount + 1, toCount: toCount + 1 };
  });
});
