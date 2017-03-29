<template>
  <el-col :span="20">
      <div class="order-header">进行中订单</div>
      
      <div class="list-content">
        <el-collapse v-model="activeNames">
          <el-collapse-item v-for="i in showItems" :name="i.id">
            <template slot="title">
              <div class="content-title">
                <div class="inner-title">桌号:{{i.table_name}}</div>
                <div class="inner-title-num">订单总数量:{{i.quantity_list.reduce((x,y)=>x+y,0)}}</div>
                <div class="inner-title-num">制作中:{{inProduction(i)}}</div>
                <div class="inner-title-num">制作完成:{{hasFinished(i)}}</div>

                <div class="inner-title-time">下单时间:{{new Date(i.create_time).toLocaleString()}}</div>
                <div class="inner-title-num">总价:¥ {{i.order_price.toFixed(2)}} 元</div>
                <div class="inner-title-num">
                  <el-button type="primary" size="small" v-on:click.stop="payOrder(i)">结账</el-button>
                  <el-button type="danger" size="small" v-on:click.stop="cancleOrder(i)">作废</el-button>
                </div>
              </div>  
            </template>
            <div class="row-content" v-for="(item,index) in i.menu_list">
              <div class="inner-content">名称：{{item.name}}</div>
              <div class="inner-content">数量：{{i.quantity_list[index]}}</div>
              <div class="inner-content">
                <el-button size="small" @click="changeState('production',i,index)" 
                :style="i.item_status_list[index]=='制作中' ? inProductionStyle: ''">制作中</el-button>
                <el-button size="small" @click="changeState('finished',i,index)"
                :style="i.item_status_list[index]=='制作完成' ? finishStyle: ''">制作完成</el-button>
              </div>
            </div>
          </el-collapse-item>
         </el-collapse> 
      </div>

      <div class="block">
        <el-pagination
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-size="pageSize"
          layout="total, prev, pager, next, jumper"
          :total="total">
        </el-pagination>
      </div>
  </el-col>
</template>

<script>
  import Vue from 'vue'
  import ApiRequest from '../common/ApiRequest.js'
  import { Message, Loading} from 'element-ui'
  export default {
    data: function(){
      return {
        total:0,
        pageSize: 20,
        currentPage: 1,
        displayItems: [],
        totalItems: [],
        activeNames: [],
        inProductionStyle: {backgroundColor:'#20a0ff',color: 'white'},
        finishStyle: {color: '#fff', backgroundColor: '#13ce66', borderColor: '#13ce66'}
      }
    },
    mounted: function(){
      let url = "order/get_all_orders";
      let loadingInstance = Loading.service({text:'加载中......'});
      let self = this;
      ApiRequest.ajGet(url, (json)=>{
        if(json.success){
          self.total = json.data.length;
          self.totalItems = json.data;
          self.displayItems = json.data.slice((self.currentPage-1)*self.pageSize, self.currentPage*self.pageSize);
          loadingInstance.close();
        }
        else{
          loadingInstance.close();
          Message.error(json.message);
        }
      })
    },
    computed:{
      showItems: function(){
        return this.displayItems;
      }
    },
    methods: {
      inProduction: function(itemList){
        let status_list = itemList['item_status_list'];
        let quantity_list = itemList['quantity_list'];
        let total = 0
        for(let i in status_list){
          if(status_list[i] == "制作中"){
            total+=quantity_list[i]
          }
        }
        return total
      },
      hasFinished: function(itemList){
        let status_list = itemList['item_status_list'];
        let quantity_list = itemList['quantity_list'];
        let total = 0
        for(let i in status_list){
          if(status_list[i] == "制作完成"){
            total+=quantity_list[i]
          }
        }
        return total
      },
      changeState: function(status,item,index){
        let item_index = this.displayItems.indexOf(item);
        let new_status;
        if(status=='production'){
          new_status = '制作中';
        }else if(status=='finished'){
          new_status = '制作完成';
        }

        // 更新状态至订单
        let oid = item.oid;
        item['item_status_list'][index] = new_status;
        let self = this;
        let url = "order/modify_order";
        let data = {oid: oid, item_status_list:item['item_status_list'], operation: 'item_status'};
        let loadingInstance = Loading.service({text:'加载中......'});
        ApiRequest.ajPost(url, data, (json)=>{
          if(json.success){
            // 通过Vue.set触发重新渲染
            Vue.set(self.displayItems[item_index]['item_status_list'], index, new_status);
            loadingInstance.close();
          }else{
            loadingInstance.close();
            Message.error(json.message);
          }
        }) 
      },
      cancleOrder:function(order){
        let oid = order.oid;
        let url = "order/modify_order";
        let data = {oid: oid, status:-1, operation: 'status'};
        let loadingInstance = Loading.service({text:'加载中......'});
        let self = this;
        ApiRequest.ajPost(url, data, (json)=>{
          if(json.success){
            let index = self.displayItems.indexOf(order);
            self.displayItems.splice(index,1);
            loadingInstance.close();
          }
          else{
            loadingInstance.close();
            Message.error(json.message);
          }
        })
      },
      payOrder:function(order){

        let item_status_list = order['item_status_list'];
        let isCompleted = item_status_list.map((item)=>{return item=='制作完成'}).reduce((pre,cur)=>{pre&&cur});
        if(!isCompleted){
          Message.info('还有未完成项，不能结算');
          return
        }else{
          console.log('paid');
        }
      },
      handleCurrentChange: function(currentPage){
        this.currentPage = parseInt(currentPage);
        this.displayItems = this.totalItems.slice((parseInt(currentPage)-1)*this.pageSize, parseInt(currentPage)*this.pageSize);
      }
    }
  }
</script>

<style scoped>
  .order-header{
    margin-left: 2%;
    padding-left: 35%;
    font-weight: 600;
    min-height: 3rem;
    line-height: 3rem;
  }
  .list-content{
    width: 96%;
    margin-left: 2%;
  }
  .content-title{
    width: 95%;
    display: inline-block;
  }
  .inner-title{
    display: inline-block;
    width: 16%;
  }
  .inner-title-time{
    display: inline-block;
    width: 20%;
  }
  .inner-title-num{
    display: inline-block;
    width: 10%;
  }
  .row-content{
    width: 100%;
  }
  .inner-content{
    display: inline-block;
    width: 33%;
    min-height: 2rem;
  }
  .block{
    width: 96%;
    margin-left: 2%;
    text-align: right;
    margin-top: 1rem;
  }

</style>