import {createApp} from 'vue'
import App from './App.vue'
// import axios from 'axios'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/es/locale/lang/zh-cn'

// axios.defaults.baseURL = 'http://127.0.0.1:5000';

// axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';


const app = createApp(App)
// app.config.globalProperties.$axios = axios;
app.use(ElementPlus, {
    locale: zhCn,
})
app.mount('#app')
