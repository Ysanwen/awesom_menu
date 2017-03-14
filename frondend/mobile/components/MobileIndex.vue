<template >
    <div id="mobile-index">
        <div id="header">
          <mt-header fixed :title="table.table_name" id="header-area"></mt-header>
        </div>
        <div id="content">
          <div class="header-picture" id="header-picture">
            <mt-swipe :auto="3000">
              <mt-swipe-item><img src="/static/upload/644887a8-fc34-11e6-879d-207c8f791ecf.jpg"></mt-swipe-item>
              <mt-swipe-item><img src="/static/upload/a43d3252-fc28-11e6-879d-207c8f791ecf.jpg"></mt-swipe-item>
            </mt-swipe>
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
                    <show-menu-item :item="con" 
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
          <div class="footer-right" v-if="totalSelectValue>0" @click="goToOrder">
            查看已选
          </div>
          <div class="footer-right" v-else @click="goToOrder">
            {{ orderItemList.length>0 ? "查看已有订单":"待点单" }}
          </div>
        </div>
    </div>
</template>

<script>
    import '../less/mobile_index.less'
    import ShowMenuItem from './ShowMenuItem.vue'

    export default{
        data:function(){
            return{
                loading:false,
                hasSelect:{backgroundColor:'#26ffa5'},
                noSelect:{backgroundColor:'#cccccc'}
            }
        },
        components:{
            ShowMenuItem
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
                  }
                }
            }
        }
    }
</script>