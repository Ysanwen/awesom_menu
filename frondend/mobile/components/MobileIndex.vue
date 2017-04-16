<template >
    <div id="mobile-index">
        <div id="header">
          <mt-header fixed :title="table.table_name" id="header-area"></mt-header>
        </div>
        <div id="content">
          <div class="header-picture" id="header-picture">
            <mt-swipe :auto="3000">
              <template v-if="indexPicture.length==0">
                <mt-swipe-item><img src="/static/demo.png"></mt-swipe-item>
              </template>
              <template v-else>
                <mt-swipe-item v-for="item in indexPicture"><img :src="'/static/upload/'+item"></mt-swipe-item>
              </template>
            </mt-swipe>
            <div class="ad">{{ad}}</div>
          </div>
          <div class="content-body">
            <div class="left-nav" id="left-nav">
              <div v-for="item in menuList" class="nav-item" @click="scrollToCenter(item)">
                {{ item }}
              </div>
            </div>
            <div class="right-content">
                <div v-for='menu_item in menuList'>
                  <a class="right-content-header" :id='"item"+menuList.indexOf(menu_item)'>{{ menu_item }}</a>
                  <div v-for="con in dataSource[menu_item]" class="inner-content" >
                    <!-- add menu item conponent -->
                    <show-menu-item :item="con" :key="con.name"
                        v-bind:defaultQuantity="selectedItemList.indexOf(con)>=0?selectedItemQuantity[selectedItemList.indexOf(con)]:0"></show-menu-item>
                  </div>
                </div> 
            </div>
          </div>
        </div>
        <div id="footer">
          <div class="footer-left" :style="totalSelectValue > 0 ? hasSelect:noSelect">
            <span class="has-choosed">当前已选{{ totalSelectValue }}份</span>
            <span>总价{{ totalPriceValue.toFixed(2) }}元</span>
          </div>
          <template v-if="totalSelectValue>0">
            <div class="footer-right" @click="goToOrder">查看已选</div>
          </template>
          <template v-else>
             <div v-if="orderItemList.length>0" class="footer-right" @click="goToOrder">查看已有订单</div>
             <div v-else class="footer-right" style="background-color: #999">待点单</div>  
          </template>
        </div>
    </div>
</template>

<script>
  import '../less/mobile_index.less'
  import ShowMenuItem from './ShowMenuItem.vue'
  import ApiRequest from '../../app/common/ApiRequest.js'

  export default{
    name: 'mobileIndex',
    data:function(){
      return{
        indexPicture:[],
        ad:'',
        restautantName:'',
        loading:false,
        hasSelect:{backgroundColor:'#26ffa5'},
        noSelect:{backgroundColor:'#cccccc'}
      }
    },
    components:{
      ShowMenuItem
    },
    created: function(){
      let url_par = this.getQueryVariable('uid');
      let url = 'user/get_restautant_info?uid=' + url_par;
      let self = this;
      ApiRequest.ajGet(url, (json)=>{
        if(json.success){
          self.indexPicture = json.data.url_list || [];
          self.ad = json.data.ad || "点菜平台";
          self.restautantName = json.data.name
        }
      })
    },
    computed:{
      menuList:function(){
        return this.$store.state.menuList;
      },
      dataSource:function(){
        return this.$store.state.dataSource;
      },
      selectedItemList:function(){
        return this.$store.state.selectedItemList;
      },
      selectedItemQuantity:function(){
        return this.$store.state.selectedItemQuantity;
        },
      totalSelectValue:function(){
        return this.$store.state.totalSelect;  
      },
      totalPriceValue:function(){
        return this.$store.state.totalPrice;
      },
      table:function(){
        return this.$store.state.table;
      },
      orderItemList:function(){
        return this.$store.state.orderItemList;            
      }
    },
    methods:{
      getQueryVariable: function(variable){
        let query = window.location.search.substring(1);
        let vars = query.split("&");
        for (let i=0;i<vars.length;i++) {
         let pair = vars[i].split("=");
         if(pair[0] == variable){return pair[1];}
        }
        return(false);
      },
      scrollToCenter:function(item){
        let index = this.menuList.indexOf(item);
        let ref_id = 'item' + index.toString();
        let el = document.getElementById(ref_id);
        let position = el.offsetTop;
        window.scrollTo(0,position);
      },
      goToOrder:function(){
        if(this.totalSelectValue>0){

          this.$store.dispatch('changeTag','order');
          this.$store.dispatch('changeShowOrder',false);
        }else{
          if(this.orderItemList.length>0){
            this.$store.dispatch('changeTag','order');
            this.$store.dispatch('changeShowOrder',true);
          }else{
            this.$store.dispatch('changeTag','order');
            this.$store.dispatch('changeShowOrder',false);
          }
        }
      }
    }
  }
</script>