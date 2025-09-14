/** @odoo-module **/

function startPaymentPolling() {
  const anchor = document.getElementById("mrcheap-payment-poll");
  if (!anchor) return;
  const txId = Number(anchor.dataset.txId || 0);
  const token = anchor.dataset.token || "";
  const txState = anchor.dataset.state || "";
  if (!txId) return;

  let stopped = false;
  const stop = () => { stopped = true; };

  const check = async () => {
    if (stopped) return;
    try {
      const url = `/mrcheap/payment_status/${txId}` + (token ? `?access_token=${encodeURIComponent(token)}` : "");
      const res = await fetch(url, { cache: "no-store" });
      const data = await res.json();

      if (data && data.ok) {
        const state = data.state;
        const paymentState = data.invoice_payment_state;
        if (paymentState === "paid") {
            window.location.reload();
            return;
        }
        if (state === "done" || state === "authorized") {
          stop();
          // Reload để hiển thị “Thank you”/nút tải hóa đơn…
          window.location.reload();
          return;
        }
        if (state === "canceled" || state === "error") {
          stop();
          // Bạn có thể show toast hoặc border đỏ, tùy ý:
          console.warn("Payment failed/canceled:", state);
          return;
        }
      }
    } catch (e) {
      console.warn("Polling error:", e);
      // Không stop; thử lại ở lần sau
    }
    // Lặp lại sau 4 giây
    if (!stopped) setTimeout(check, 4000);
  };

  check();
}

document.addEventListener("DOMContentLoaded", startPaymentPolling);
