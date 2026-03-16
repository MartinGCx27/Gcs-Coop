// Set your publishable key: remember to change this to your live publishable key in production
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = Stripe('pk_test_51J8dDBCor9GAAV0ad6MbhgeYe7B84iHhSLGpYQaUJoqimGGqQElosC5q9MI3OjisDEqE92yjQoDuDcE9yqRVklJP00qAgS2FnZ');

const options = {
  clientSecret: '{{CLIENT_SECRET}}',
  // Fully customizable with appearance API.
  appearance: {/.../},
};

// Set up Stripe.js and Elements to use in checkout form, passing the client secret obtained in step 2
const elements = stripe.elements(options);

// Create and mount the Payment Element
const paymentElement = elements.create('payment');
paymentElement.mount('#payment-element');






//const appearance = {
//  theme: 'minimal',
//  variables: {
//    fontFamily: ' "bigcalson", "Bodoni",
//    cssSrc: 'static/css/style_font.css'
//    fontLineHeight: '1.5',
//    borderRadius: '10px',
//    colorBackground: '#F6F8FA',
//    colorPrimaryText: '#262626'
//  },
//  ': {rules: {
//    '.Block
//      backgroundColor: 'var(--colorBackground)',
//      boxShadow: 'none',
//      padding: '12px'
//    },
//    '.Input': {
//      padding: '12px'
//    },
//    '.Input:disabled, .Input--invalid:disabled': {
//      color: 'lightgray'
//    },
//    '.Tab': {
//      padding: '10px 12px 8px 12px',
//      border: 'none'
//    },
//    '.Tab:hover': {
//      border: 'none',
//      boxShadow: '0px 1px 1px rgba(0, 0, 0, 0.03), 0px 3px 7px rgba(18, 42, 66, 0.04)'
//    },
//    '.Tab--selected, .Tab--selected:focus, .Tab--selected:hover': {
//      border: 'none',
//      backgroundColor: '#fff',
//      boxShadow: '0 0 0 1.5px var(--colorPrimaryText), 0px 1px 1px rgba(0, 0, 0, 0.03), 0px 3px 7px rgba(18, 42, 66, 0.04)'
//    },
//    '.Label': {
//      fontWeight: '500'
//    }
//  }
//};
//
//// Pass the appearance object to the Elements instance
//const elements = stripe.elements({clientSecret, appearance});




//
//// A reference to Stripe.js initialized with a fake API key.
//
//const stripe = Stripe("pk_test_51J8dDBCor9GAAV0ad6MbhgeYe7B84iHhSLGpYQaUJoqimGGqQElosC5q9MI3OjisDEqE92yjQoDuDcE9yqRVklJP00qAgS2FnZ");
//
//// The items the customer wants to buy
//const items = [{ id: "xl-tshirt" }];
//
//let elements;
//
//initialize();
//checkStatus();
//
//document
//  .querySelector("#payment-form")
//  .addEventListener("submit", handleSubmit);
//
//// Fetches a payment intent and captures the client secret
//async function initialize() {
//  const response = await fetch("/create-payment-intent", {
//    method: "POST",
//    headers: { "Content-Type": "application/json" },
//    body: JSON.stringify({ items }),
//  });
//  const { clientSecret } = await response.json();
//
//  const appearance = {
//    theme: 'stripe',
//  };
//  elements = stripe.elements({ appearance, clientSecret });
//
//  const paymentElement = elements.create("payment");
//  paymentElement.mount("#payment-element");
//}
//
//async function handleSubmit(e) {
//  e.preventDefault();
//  setLoading(true);
//
//  const { error } = await stripe.confirmPayment({
//    elements,
//    confirmParams: {
//      // Make sure to change this to your payment completion page
//      return_url: "http://localhost:4242/checkout.html",
//    },
//  });
//
//  // This point will only be reached if there is an immediate error when
//  // confirming the payment. Otherwise, your customer will be redirected to
//  // your `return_url`. For some payment methods like iDEAL, your customer will
//  // be redirected to an intermediate site first to authorize the payment, then
//  // redirected to the `return_url`.
//  if (error.type === "card_error" || error.type === "validation_error") {
//    showMessage(error.message);
//  } else {
//    showMessage("An unexpected error occured.");
//  }
//
//  setLoading(false);
//}
//
//// Fetches the payment intent status after payment submission
//async function checkStatus() {
//  const clientSecret = new URLSearchParams(window.location.search).get(
//    "payment_intent_client_secret"
//  );
//
//  if (!clientSecret) {
//    return;
//  }
//
//  const { paymentIntent } = await stripe.retrievePaymentIntent(clientSecret);
//
//  switch (paymentIntent.status) {
//    case "succeeded":
//      showMessage("Payment succeeded!");
//      break;
//    case "processing":
//      showMessage("Your payment is processing.");
//      break;
//    case "requires_payment_method":
//      showMessage("Your payment was not successful, please try again.");
//      break;
//    default:
//      showMessage("Something went wrong.");
//      break;
//  }
//}
//
//// ------- UI helpers -------
//
//function showMessage(messageText) {
//  const messageContainer = document.querySelector("#payment-message");
//
//  messageContainer.classList.remove("hidden");
//  messageContainer.textContent = messageText;
//
//  setTimeout(function () {
//    messageContainer.classList.add("hidden");
//    messageText.textContent = "";
//  }, 4000);
//}
//
//// Show a spinner on payment submission
//function setLoading(isLoading) {
//  if (isLoading) {
//    // Disable the button and show a spinner
//    document.querySelector("#submit").disabled = true;
//    document.querySelector("#spinner").classList.remove("hidden");
//    document.querySelector("#button-text").classList.add("hidden");
//  } else {
//    document.querySelector("#submit").disabled = false;
//    document.querySelector("#spinner").classList.add("hidden");
//    document.querySelector("#button-text").classList.remove("hidden");
//  }
//}