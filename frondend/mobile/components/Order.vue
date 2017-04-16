<template>
  <div id="mobile-order">
    <div class="header">
      <mt-header fixed :title="table.table_name" id="header-area"></mt-header>
    </div>
    <div class="header-nav">
      <mt-button class="button-menu" type="default" @click="goToIndex">继续点单</mt-button>
      <mt-button class="button-menu" :type="showOrder?'default':'primary'" @click="showSlected">当前已选</mt-button>
      <mt-button class="button-menu" :type="showOrder?'primary':'default'" @click="showOrders">已点订单</mt-button>  
    </div>
    <div v-if="showOrder" class="content order-content">
      <template v-if="orderItemList.length>0">
        <div v-for='(con,index) in orderItemList' class="order-item">
          <!-- add menu item conponent -->
          <show-menu-item :item="con" v-bind:defaultQuantity='orderItemQuantity[index]' :key="con.name+'s'"></show-menu-item>
        </div>
      </template>
      <template v-else>
        <div class="no-order-content">
          还没点单，<span class="make-order" @click="goToIndex">现在点单</span>
        </div>            
      </template>
    </div>
    <div v-else class="content order-content">
      <template v-if="selectedItemList.length>0">
        <div v-for='(con,index) in selectedItemList' class="order-item">
          <!-- add menu item conponent -->
          <show-menu-item :item="con" v-bind:defaultQuantity='selectedItemQuantity[index]' :key="con.name+'n'"></show-menu-item>
        </div>
      </template>
      <template v-else>
        <div class="no-order-content">
          没有在选内容，<span class="make-order" @click="goToIndex">继续选择</span>
        </div>            
      </template>
    </div>
    <div v-if="showOrder" id="footer">
      <div class="footer-left" :style="totalOrderQuantity > 0 ? hasSelect:noSelect">
        <span class="has-choosed">已选{{ totalOrderQuantity }}份</span>
        <span>总价{{ totalOrderPrice.toFixed(2) }}元</span>
      </div>
      <div v-if="totalOrderQuantity > 0" class="footer-right" @click="PayOrder">支付</div>
      <div v-else class="footer-right un-click">支付</div>
    </div>
    <div v-else id="footer">
      <div class="footer-left" :style="totalSelectValue > 0 ? hasSelect:noSelect">
        <span class="has-choosed">已选{{ totalSelectValue }}份</span>
        <span>总价{{ totalPriceValue.toFixed(2) }}元</span>
      </div>
      <div v-if="totalSelectValue>0" class="footer-right" @click="submitOrder">确认下单</div>
      <div v-else class="footer-right un-click">还未选单</div>
    </div>
  </div>
</template>

<script>
  import { Toast } from 'mint-ui'
  import ShowMenuItem from './ShowMenuItem.vue'
  import ApiRequest from '../../app/common/ApiRequest.js'

  export default{
    name:'order',
    components:{
      ShowMenuItem
    },
    data:function(){
      return{
        hasSelect:{backgroundColor:'#26ffa5'},
        noSelect:{backgroundColor:'#cccccc'}
      }
    },
    computed:{
      userId:function(){
        return this.$store.state.userId;
      },
      table:function(){
        return this.$store.state.table;
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
      orderItemList:function(){
        return this.$store.state.orderItemList;
      },
      orderItemQuantity:function(){
        return this.$store.state.orderItemQuantity;
      },
      showOrder:function(){
        return this.$store.state.showOrder;
      },
      totalOrderQuantity:function(){
        return this.$store.state.orderItemQuantity.reduce((x,y)=>x+y,0);
      },
      totalOrderPrice:function(){
        let menus = this.$store.state.orderItemList;
        let quantity_list = this.$store.state.orderItemQuantity;
        let total_price = 0;
        if(quantity_list.length>0){

          for(let item=0;item<quantity_list.length;item++){
            total_price += menus[item]['price'] * quantity_list[item];
          }
          return total_price;
        }else{
          return 0;
        }
      }
    },
    methods:{
      goToIndex:function(){
        this.$store.dispatch('changeTag','index');
        this.$store.dispatch('changeShowOrder',false);
      },
      PayOrder:function(){
        Toast({
          message: '请至收银台结算',
          duration: 2000
        });
      },
      submitOrder:function(){
        let menu_list = this.selectedItemList;
        if(menu_list.length>0){

          let quantity_list = this.selectedItemQuantity;
          let table_id = this.table.table_id;
          let table_name = this.table.table_name;
          let order_price = this.totalPriceValue;
          let uid = this.userId;
          let post_data = {uid:uid,menu_list:menu_list,quantity_list:quantity_list,table_id:table_id,table_name:table_name,order_price:order_price};

          let url;
          if(this.orderItemList.length>0){
            url = 'order/update_order';
          }else{
            url = 'order/create_order';
          }

          let that = this;

          ApiRequest.ajPost(url,post_data,(json)=>{
            if(json.success){      
              Toast({
                message: '下单成功',
                duration: 1000
              });
              that.$store.dispatch('moveSelectedToOrder');
              that.$store.dispatch('changeShowOrder',true);
            }else{
              alert(json.message);
            }
          })
        }

      },

      showSlected:function(){
        this.$store.dispatch('changeShowOrder',false);
      },
      showOrders:function(){
        this.$store.dispatch('changeShowOrder',true);
      }
    },
    created:function(){
      window.scrollTo(0,0);
    }
  }
</script>
<style>
  .header-nav{
    margin-top: 40px;
    height: 4rem;
    line-height: 4rem;
    text-align: center;
    position: fixed;
    width: 100%;
    z-index: 1;
    background-color: white;
  }
  .button-menu{
    font-size: 0.85rem;
    width: 30%;
  }
  .order-content{
    width: 100%;
    margin-top: 6.5rem;
    margin-left: 0.5rem;
    position: absolute;
    margin-bottom: 2.5rem;
  }
  .no-order-content{
    width: 100%;
    height: 6rem;
    line-height: 6rem;
    text-align: center;
    color: #999;
  }
  .make-order{
    color: rgba(0, 0, 255, 0.55);
  }
  .order-content .food-img{
    width: 30%;
  }
  .order-item{
    border-bottom: 1px solid #eaeaea;
    margin-top: 2px;
    min-height: 6rem;
  }
  .order-content .food-content{
    width: 65%;
    float: right;
  }
  .un-click{
    background-color: #999 !important;
  }
</style>