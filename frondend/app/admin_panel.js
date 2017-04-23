import Vue from 'vue'
import VueRouter from 'vue-router'
import VueSocketio from 'vue-socket.io'
import { Row,Col,Menu,Submenu,MenuItem,MenuItemGroup,Dropdown,Button,DropdownItem,DropdownMenu, Collapse,CollapseItem,Pagination,Radio,RadioGroup} from 'element-ui'
import { Message } from 'element-ui'
import './admin_panel.less'
import LeftNav from './components/LeftNav.vue'
import ApiRequest from './common/ApiRequest.js'
import AddMenu from './components/AddMenu.vue'
import AllMenu from './components/AllMenu.vue'
import QrcodeMenu from './components/QrcodeMenu.vue'
import Orders from './components/Orders.vue'
import FinishedOrder from './components/FinishedOrder.vue'
import RestaurantInfo from './components/RestaurantInfo.vue'

let import_list = [Row,Col,Menu,Submenu,MenuItem,MenuItemGroup,Dropdown,Button,DropdownItem,DropdownMenu,Collapse,CollapseItem,Pagination,Radio,RadioGroup]
for (let item in import_list){
  Vue.use(import_list[item])
} 

Vue.use(VueRouter);
Vue.use(VueSocketio, '127.0.0.1:5000');

const router = new VueRouter({
  routes:[
    { path: '/', component: AllMenu},
    { path: '/allMenu', component: AllMenu },
    { path: '/addMenu', name:'addMenu', component: AddMenu },
    { path: '/qrcodeMenu', component: QrcodeMenu },
    { path: '/allOrder', component: Orders},
    { path: '/finishedOrder', component: FinishedOrder},
    { path: '/restaurantInfo', name:'restaurantInfo',  component: RestaurantInfo}
  ]
});

let ap = new Vue({
  router,
  el:'#admin_panel',
  data:{
    username:'xxx',
    current_user: '',
    dropDownStyle:{
      display:'none'
    }
  
  },
  components:{
    LeftNav,AddMenu
  },
  methods:{
    showDropDown: function(){
      this.dropDownStyle={display: 'block'}
    },
    hideDropDown: function(){
      this.dropDownStyle={display: 'none'}  
    },
    setInfo: function(){
      this.$router.push({name:'restaurantInfo'})
    },
    signOut: function(){
      ApiRequest.ajGet('sign_out', (json)=>{
        if(json.success){
          window.location.href = '/' + json.redirect_url
        }else{
          Message.error(json.message)
        }
      })
    }
  },
  created: function(){
    let self = this;
    ApiRequest.ajGet('user/get_current_user',(json)=>{
      if(json.success){
        self.username = json.data.username==''?json.data.mobile:json.data.username
        self.current_user = json.data;
      }else{
        Message.error(json.message)
      }
    })
  }
})