
// import { configureStore } from "@reduxjs/toolkit";
// import authReducer from "./slices/authSlice";
// import newsReducer from "./slices/newsSlice";
// import uiReducer from "./slices/uiSlice";

// export const store = configureStore({
//   reducer: {
//     auth: authReducer,
//     news: newsReducer,
//     ui: uiReducer,
//   },
// });

// export type RootState = ReturnType<typeof store.getState>;
// export type AppDispatch = typeof store.dispatch;

import { configureStore } from "@reduxjs/toolkit";
import authReducer from "./slices/authSlice";

export const store = configureStore({
  reducer: {
    auth: authReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;


