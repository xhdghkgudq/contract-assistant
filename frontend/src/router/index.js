import { createRouter, createWebHistory } from "vue-router";
import Login from "../views/Login.vue";
import Home from "../views/Home.vue";
import Upload from "../views/Upload.vue";
import Review from "../views/Review.vue";
import ContractList from "../views/ContractList.vue";
import Dashboard from "../views/Dashboard.vue";

const routes = [
  { path: "/", component: Login, meta: { requiresAuth: false } },
  { path: "/home", component: Home, meta: { requiresAuth: true } },
  { path: "/upload", component: Upload, meta: { requiresAuth: true } },
  { path: "/review", component: Review, meta: { requiresAuth: true } },
  { path: "/dashboard", component: Dashboard, meta: { requiresAuth: true } },
  { path: "/contracts", component: ContractList, meta: { requiresAuth: true } },
  { path: "/:pathMatch(.*)*", redirect: "/", meta: { requiresAuth: false } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const requiresAuth = to.meta?.requiresAuth ?? true;

  if (!requiresAuth) {
    // 不需要认证的页面（只有登录页）
    const token = localStorage.getItem("token");
    const userStr = localStorage.getItem("user");
    if (token && userStr && to.path === "/") {
      // 如果已经登录，访问登录页则跳转到主页
      next("/home");
      return;
    }
    next();
    return;
  }

  // 需要认证的页面
  const token = localStorage.getItem("token");
  const userStr = localStorage.getItem("user");

  // 检查token和用户信息
  if (!token || !userStr) {
    console.log("未登录，重定向到登录页");
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    next("/");
    return;
  }

  // 验证用户信息是否有效
  try {
    const user = JSON.parse(userStr);
    if (!user.id || !user.username || !user.role) {
      console.log("用户信息无效，重定向到登录页");
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      next("/");
      return;
    }
  } catch (e) {
    console.log("用户信息解析失败，重定向到登录页");
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    next("/");
    return;
  }

  next();
});

export default router;
