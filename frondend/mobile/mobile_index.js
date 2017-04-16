import Vue from 'vue'
import MintUI from 'mint-ui'
import 'mint-ui/lib/style.css'
import 'material-design-icons/iconfont/material-icons.css'

import MobileIndex from './components/MobileIndex.vue'
import Order from './components/Order.vue'
import store from './store/store.js'


Vue.use(MintUI);
// Vue.component(Header.name, Header);

var mobile_app = new Vue({
  name:'index',
  el:'#mobile',
  store,
  components:{
    MobileIndex,
    Order
  },
  created:function () {
    store.dispatch('initData');
  },
  computed:{
    showTag:function(){
      return store.state.showTag;
    }
  }
});