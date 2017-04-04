import Vue from 'vue'
import VueRouter from 'vue-router'
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

let import_list = [Row,Col,Menu,Submenu,MenuItem,MenuItemGroup,Dropdown,Button,DropdownItem,DropdownMenu,Collapse,CollapseItem,Pagination,Radio,RadioGroup]
for (let item in import_list){
    Vue.use(import_list[item])
} 

Vue.use(VueRouter);

const router = new VueRouter({
  routes:[
      { path: '/', component: AllMenu},
      { path: '/allMenu', component: AllMenu },
      { path: '/addMenu', name:'addMenu', component: AddMenu },
      { path: '/qrcodeMenu', component: QrcodeMenu },
      { path: '/allOrder', component: Orders},
      { path: '/finishedOrder', component: FinishedOrder}
  ]
});

let ap = new Vue({
    router,
    el:'#admin_panel',
    data:{
        username:'xxx',
        dropDownStyle:{
            display:'none'
        }
    
    },
    components:{
        LeftNav,AddMenu
    },
    methods:{
        showDropDown:function(){
            this.dropDownStyle={display:'block'}
        },
        hideDropDown:function(){
            this.dropDownStyle={display:'none'}  
        },
        signOut:function(){
            console.log('sign_out');
            ApiRequest.ajGet('sign_out',(json)=>{
                if(json.success){
                    window.location.href='/'+json.redirect_url
                }else{
                    Message.error(json.message)
                }
            })
        }
    },
    created:function(){
        ApiRequest.ajGet('user/get_current_user',(json)=>{
            if(json.success){
                ap.username = json.data.username=='unknow'?json.data.mobile:json.data.username
            }else{
                Message.error(json.message)
            }
        })
    }
})