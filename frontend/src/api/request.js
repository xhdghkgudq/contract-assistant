import axios from "axios";

const request = axios.create({
  baseURL: "http://localhost:5000",
  withCredentials: true,
});

// 添加请求拦截器，携带认证令牌
request.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers["Authorization"] = `Bearer ${token}`;
    }
    // 如果是 FormData，删除Content-Type让浏览器自动处理（包括boundary）
    if (config.data instanceof FormData) {
      delete config.headers["Content-Type"];
    } else if (!config.headers["Content-Type"]) {
      // 默认使用 JSON 格式
      config.headers["Content-Type"] = "application/json";
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

// 添加响应拦截器，处理错误
request.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error("请求错误:", error);
    console.error("错误详情:", error.response);
    return Promise.reject(error);
  },
);

export default request;
