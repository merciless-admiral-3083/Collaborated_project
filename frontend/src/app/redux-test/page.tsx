"use client";
import { useAppDispatch, useAppSelector } from "@/store/hooks";
import { login, logout } from "@/store/slices/userSlice";

export default function ReduxTest() {
  const dispatch = useAppDispatch();
  const user = useAppSelector((state) => state.user);

  return (
    <div style={{ padding: "20px" }}>
      <h1>Redux Test</h1>

      <button
        onClick={() =>
          dispatch(login({ username: "maryha", token: "123456" }))
        }
      >
        Login
      </button>

      <button onClick={() => dispatch(logout())}>
        Logout
      </button>

      <pre>{JSON.stringify(user, null, 2)}</pre>
    </div>
  );
}
