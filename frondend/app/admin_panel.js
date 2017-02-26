import Vue from 'vue'
import VueRouter from 'vue-router'
import { Row,Col,Menu,Submenu,MenuItem,MenuItemGroup,Dropdown,Button,DropdownItem,DropdownMenu} from 'element-ui'
import { Message } from 'element-ui'
import './admin_panel.less'
import LeftNav from './components/LeftNav.vue'
import ApiRequest from './common/ApiRequest.js'
import AddMenu from './components/AddMenu.vue'
import AllMenu from './components/AllMenu.vue'

let import_list = [Row,Col,Menu,Submenu,MenuItem,MenuItemGroup,Dropdown,Button,DropdownItem,DropdownMenu]
for (let item in import_list){
    Vue.use(import_list[item])
} 

Vue.use(VueRouter);

// const Bar = { template: '<div>addMenu</div>' };

const router = new VueRouter({
  routes:[
      { path: '/allMenu', component: AllMenu },
      { path: '/addMenu', component: AddMenu }
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
    },
    // computed:{
    //     username:function(){
    //         console.log('computed')
    //         return 'ss'
    //     }
    // }
})