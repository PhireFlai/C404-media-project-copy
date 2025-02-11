import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const api = createApi({
  reducerPath: "api",
  baseQuery: fetchBaseQuery({ baseUrl: "http://127.0.0.1:8000/" }),
  endpoints: (builder) => ({
    getTest: builder.query({
      query: () => "core/test",
    }),
  }),
});

export const { useGetTestQuery } = api;
