import request from "./request";

export const uploadApi = (file) => {
  const formData = new FormData();
  formData.append("file", file);

  return request.post("/upload", formData);
};
