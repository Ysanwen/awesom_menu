import Vue from 'vue'
import MintUI from 'mint-ui'
import 'mint-ui/lib/style.css'
import './mobile_index.less'

import Lodash from 'lodash'

Vue.use(MintUI);
// Vue.component(Header.name, Header);

var mobile_app = new Vue({
    el:'#mobile',
    data:function(){
        return{
            menuList:['菜单一','菜单二','菜单三','菜单四','菜单五'],
            foodList:[{name:'炒肉',type:'小炒',quantity:100,price:15}],
            loading:false,
            navStyle:{position:'relative',top:'0px'}
        }
    },
    methods:{
        
    },
    created:function(){
        // listen to the scroll and set the nav style
        window.addEventListener('scroll',Lodash.throttle(function(){
            let head_height = document.getElementById("header-area").offsetHeight;
            // let scroll_top = Math.max(document.body.scrollTop,document.documentElement.scrollTop);
            let nav_el = document.getElementById("header-picture");
            let nav_height = nav_el.getBoundingClientRect().bottom;
            if(parseInt(nav_height) <= parseInt(head_height)+20){
                mobile_app.navStyle = {position:'fixed',top:head_height+'px'};
            }else{
                mobile_app.navStyle = {position:'relative',top:'0px'};
            }
           
        }),10);
    }
});