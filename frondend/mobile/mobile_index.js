import Vue from 'vue'
import MintUI from 'mint-ui'
import 'mint-ui/lib/style.css'
import './mobile_index.less'
import ApiRequest from '../app/common/ApiRequest.js'
import 'material-design-icons/iconfont/material-icons.css'

import Lodash from 'lodash'

Vue.use(MintUI);
// Vue.component(Header.name, Header);

var mobile_app = new Vue({
    el:'#mobile',
    data:function(){
        return{
            menuList:['菜单一','菜单二','菜单三','菜单四','菜单五'],
            dataSource:[],
            loading:false,
        }
    },
    methods:{
        
    },
    created:function(){
        let getQueryVariable = function(variable){
            var query = window.location.search.substring(1);
            var vars = query.split("&");
            for (var i=0;i<vars.length;i++) {
                   var pair = vars[i].split("=");
                   if(pair[0] == variable){return pair[1];}
            }
            return(false);
        }
        let url_par = getQueryVariable('uid');
        ApiRequest.ajGet('category/get_categories_menu?uid='+url_par,(json)=>{
            if(json.success){
                mobile_app.menuList = json.data.category;
                mobile_app.dataSource = json.data;
            }else{
                alert(json.message)
            }
        })
        // listen to the scroll and set the nav style
        // window.addEventListener('touchmove',Lodash.throttle(function(){
        //     let head_height = document.getElementById("header-area").offsetHeight;
        //     // let scroll_top = Math.max(document.body.scrollTop,document.documentElement.scrollTop);
        //     let nav_el = document.getElementById("header-picture");
        //     let nav_height = nav_el.getBoundingClientRect().bottom;
        //     if(parseInt(nav_height) <= parseInt(head_height)+20){
        //         mobile_app.navStyle = {position:'fixed',top:head_height+'px'};
        //     }else{
        //         mobile_app.navStyle = {position:'relative',top:'0px'};
        //     }
           
        // }),10);
    }
});