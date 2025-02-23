import axios from axios;
const axiosInstance = axios.create({
 baseURL: "https://api.example.com", // Replace with your API base URL
 headers: {
   "Content-Type": "application/json",
   // Add any other headers or configurations you need
 },
});

// Add a request interceptor
axiosInstance.interceptors.request.use(
 (config) => {
   // You can modify the request config here, e.g., add authentication headers
   // config.headers.Authorization = `Bearer ${getToken()}`;
   return config;
 },
 (error) => {
   return Promise.reject(error);
 }
);

// Add a response interceptor
axiosInstance.interceptors.response.use(
 (response) => {
   // You can modify the response data here, e.g., handling pagination
   return response.data;
 },
 (error) => {
   return Promise.reject(error);
 }
);

export default axiosInstance;