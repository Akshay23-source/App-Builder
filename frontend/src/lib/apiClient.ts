import axios from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    "Content-Type": "application/json",
  },
});

apiClient.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    let token = localStorage.getItem("forgeai_token");
    if (!token) {
      token = "dev_mock_token_12345";
      localStorage.setItem("forgeai_token", token);
    }
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
