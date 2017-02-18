import Vue from 'vue'
import { Row,Col,Menu,SubMenu,MenuItem,MenuItemGroup,Dropdown,Button,DropdownItem,DropdownMenu,Message} from 'element-ui'
import './admin_panel.less'
import LeftNav from './components/LeftNav.vue'
import ApiRequest from './common/ApiRequest.js'

let import_list = [Row,Col,Menu,SubMenu,MenuItem,MenuItemGroup,Dropdown,Button,DropdownItem,DropdownMenu,Message]
for (let item in import_list){
    Vue.use(import_list[item])
} 

let ap = new Vue({
    el:'#admin_panel',
    data:{
        username:'xxx'
    },
    components:{
        LeftNav
    },
    methods:{

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