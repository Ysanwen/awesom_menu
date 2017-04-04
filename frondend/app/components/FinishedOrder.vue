<template>
  <el-col :span="20">
      <div class="order-header">已完成订单</div>
      
      <div class="list-content">
        <el-collapse v-model="activeNames">
          <el-collapse-item v-for="i in displayItems" :name="i.id"  id="my-title">
            <template slot="title">
              <div class="content-title">
                <div class="inner-title">桌号:{{i.table_name}}</div>
                <div class="inner-title-num">订单总数量:{{i.quantity_list.reduce((x,y)=>x+y,0)}}</div>

                <div class="inner-title-time">下单时间:{{new Date(i.create_time).toLocaleString()}}</div>
                <div class="inner-title-time">完成时间:{{new Date(i.paid_time).toLocaleString()}}</div>
                <div class="inner-title-num">总价:¥ {{i.order_price.toFixed(2)}} 元</div>
                <div class="inner-title-num">实收:¥ {{i.actuality_paid.toFixed(2)}} 元</div>
                
              </div>  
            </template>
            <div class="row-content" v-for="(item,index) in i.menu_list">
              <div class="inner-content">名称：{{item.name}}</div>
              <div class="inner-content">数量：{{i.quantity_list[index]}}</div>
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
  import ApiRequest from '../common/ApiRequest.js' 
  export default {
    data: function(){
      return {
        activeNames:[],
        displayItems: [],
        currentPage: 1,
        pageSize: 20,
        total: 0

      }
    },
    created: function(){
      this.search();
    },
    methods: {
      handleCurrentChange: function(page){
        this.currentPage = page;
        this.search();
      },
      search: function(){
        let url = 'order/get_finished_orders?currentPage=' + this.currentPage + '&pageSize=' + this.pageSize;
        let self = this;
        ApiRequest.ajGet(url, (json)=>{
          self.displayItems = json.data.data;
          self.total = json.data.total;
        })
      }
    }
  }
</script>

<style>
  .order-header{
    margin-left: 2%;
    padding-left: 35%;
    font-weight: 600;
    min-height: 3rem;
    line-height: 3rem;
  }
  #my-title .el-collapse-item__header{
    height: initial !important;
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