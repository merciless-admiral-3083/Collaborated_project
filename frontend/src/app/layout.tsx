// "use client";

// import { Provider } from "react-redux";
// import { store } from "@/store/store";

// export default function RootLayout({ children }: { children: React.ReactNode }) {
//   return (
//     <html lang="en">
//       <body>
//         <Provider store={store}>
//           {children}
//         </Provider>
//       </body>
//     </html>
//   );
// }

"use client";

import { Provider } from "react-redux";
import { store } from "@/store/store";   // ✅ correct now

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Provider store={store}>{children}</Provider>
      </body>
    </html>
  );
}


