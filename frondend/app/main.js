import Vue from 'vue'
// import 'element-ui/lib/theme-default/index.css'
import { Button,Dialog,Form,Input,FormItem } from 'element-ui'
import './main.less'

import SignComponent from './components/SignComponent.vue'

Vue.use(Button);
Vue.use(Dialog);
Vue.use(Form);
Vue.use(FormItem);
Vue.use(Input);

var ap = new Vue({
    el: '#app',
    data: {
        message: 'Awesome !!!',
        showDialog: false,
        clickType:''
    },
    components:{
        SignComponent
    },
    methods:{
        popup_sign_in:function(){
            this.showDialog = !this.showDialog;
            this.clickType = 'sign_in';
            
        },
        popup_sign_up:function(){
            this.showDialog = !this.showDialog;
            this.clickType = 'sign_up'  
        }
    }
});

// ap.message = 'qqq';