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
