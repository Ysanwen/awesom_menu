<template>
    <div id="mobile-order">
        <div class="header">
          <mt-header fixed :title="table.table_name" id="header-area"></mt-header>
        </div>
        <div class="header-nav">
          <mt-button type="default" @click="goToIndex">继续点单</mt-button>
          <mt-button type="primary">当前已点</mt-button>
          
        </div>
        <div class="content order-content">
          <div v-for='(con,index) in selectedItemList'>
            <!-- add menu item conponent -->
            <show-menu-item :item="con" v-bind:defaultQuantity='selectedItemQuantity[index]'></show-menu-item>
          </div>
        </div>
        <div id="footer">
          <div class="footer-left" :style="totalSelectValue > 0 ? hasSelect:noSelect">
            <span class="has-choosed">已选{{ totalSelectValue }}份</span>
            <span>总价{{ totalPriceValue.toFixed(2) }}元</span>
          </div>
          <div class="footer-right" @click="submitOrder">确认下单</div>
        </div>
    </div>
</template>

<script>
  import { Toast } from 'mint-ui'
  import ShowMenuItem from './ShowMenuItem.vue'
  import ApiRequest from '../../app/common/ApiRequest.js'

  export default{
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
      }
    },
    methods:{
      goToIndex:function(){
        this.$store.dispatch('changeTag','index');
      },
      submitOrder:function(){
        let menu_list = this.selectedItemList;
        let quantity_list = this.selectedItemQuantity;
        let table_id = this.table.table_id;
        let table_name = this.table.table_name;
        let order_price = this.totalPriceValue;

        let post_data = {menu_list:menu_list,quantity_list:quantity_list,table_id:table_id,table_name:table_name,order_price:order_price};
        let url = 'order/create_order';

        ApiRequest.ajPost(url,post_data,(json)=>{
          if(json.success){
            console.log(json.data);
            Toast({
              message: '下单成功',
              duration: 1000
            });
          }else{
            alert(json.message);
          }
        })

      }
    }
  }
</script>
<style scoped>
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
  .order-content{
    margin-top: 6.5rem;
    margin-left: 0.5rem;
    position: absolute;
    margin-bottom: 2.5rem;
  }
  .order-content .food-img{
    width: 30%;
  }
  .order-content .food-content{
    width: 65%;
    float: right;
  }
</style>