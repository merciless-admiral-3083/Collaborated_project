import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";

interface NewsState {
  global: any;
  history: any[];
  loading: boolean;
  error: string | null;
}

const initialState: NewsState = {
  global: null,
  history: [],
  loading: false,
  error: null,
};

export const fetchGlobalSummary = createAsyncThunk(
  "news/global",
  async (_, thunkAPI) => {
    try {
      const res = await fetch("http://localhost:8000/api/global_summary");
      const data = await res.json();
      if (!res.ok) return thunkAPI.rejectWithValue(data.detail);
      return data;
    } catch {
      return thunkAPI.rejectWithValue("Failed to fetch global summary");
    }
  }
);

export const fetchHistory = createAsyncThunk(
  "news/history",
  async (country: string, thunkAPI) => {
    try {
      const res = await fetch(
        `http://localhost:8000/api/history/${country}?days=30`
      );
      const data = await res.json();
      if (!res.ok) return thunkAPI.rejectWithValue(data.detail);
      return data;
    } catch {
      return thunkAPI.rejectWithValue("Failed to fetch history data");
    }
  }
);

const newsSlice = createSlice({
  name: "news",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchGlobalSummary.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchGlobalSummary.fulfilled, (state, action) => {
        state.loading = false;
        state.global = action.payload;
      })
      .addCase(fetchGlobalSummary.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      .addCase(fetchHistory.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchHistory.fulfilled, (state, action) => {
        state.loading = false;
        state.history = action.payload;
      })
      .addCase(fetchHistory.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});

export default newsSlice.reducer;
