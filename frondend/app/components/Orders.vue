<template>
  <el-col :span="20">
      <div class="order-header">进行中订单</div>
      
      <div class="list-content">
        <el-collapse v-model="activeNames" @change="handleChange">
          <el-collapse-item v-for="i in displayItems" :name="i.id">
            <template slot="title">
              <div class="content-title">
                <div class="inner-title">桌号:{{i.table_name}}</div>
                <div class="inner-title-num">订单总数量:{{i.quantity_list.reduce((x,y)=>x+y,0)}}</div>
                <div class="inner-title-num">制作中:</div>
                <div class="inner-title-num">制作完成:</div>

                <div class="inner-title-time">下单时间:{{new Date(i.create_time).toLocaleString()}}</div>
                <div class="inner-title-num">总价:¥ {{i.order_price.toFixed(2)}} 元</div>
                <div class="inner-title-num">操作</div>
              </div>  
            </template>
            <div class="row-content" v-for="item in i.menu_list">
              <div class="inner-content">名称：{{item.name}}</div>
              <div class="inner-content">数量：{{i.quantity_list[item.id-1]}}</div>
              <div class="inner-content">操作：</div>
            </div>
          </el-collapse-item>
         </el-collapse> 
      </div>

      <div class="block">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-size="10"
          layout="total, prev, pager, next, jumper"
          :total="100">
        </el-pagination>
      </div>
  </el-col>
</template>

<script>
  import ApiRequest from '../common/ApiRequest.js'
  import { Message, Loading} from 'element-ui'
  export default {
    data: function(){
      return {
        total:'',
        pageSize: 10,
        currentPage: 1,
        displayItems: [],
        totalItems: [],
        activeNames: []
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
    methods: {
      handleChange: function(activeNames){
        console.log(activeNames);
      },
      handleSizeChange: function(size){
        // call this function when per page size changed
        console.log(size)
      },
      handleCurrentChange: function(currentPage){
        self.currentPage = parseInt(currentPage);
        self.displayItems = self.totalItems.slice((parseInt(currentPage)-1)*self.pageSize, parseInt(currentPage)*self.pageSize);
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
  }
  .block{
    width: 96%;
    margin-left: 2%;
    text-align: right;
    margin-top: 1rem;
  }

</style>