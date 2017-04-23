<template>
  <el-col :span="20">
      <div class="order-header">进行中订单</div>
      
      <div class="list-content">
        <el-collapse v-model="activeNames">
          <el-collapse-item v-for="i in displayItems" :name="i.id" id="my-title">
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

      <el-dialog title="结算" v-model="dialogVisible" size="tiny">
      <div>
        <span>付款方式：</span>
        <el-radio-group v-model="payType">
          <el-radio label="现金">现金</el-radio>
          <el-radio label="支付宝">支付宝</el-radio>
          <el-radio label="微信">微信</el-radio>
          <el-radio label="刷卡">刷卡</el-radio>
        </el-radio-group>
      </div>
      <div class="pay-form">  
        <span>订单金额：{{' ' + parseFloat(currentOrder['order_price']).toFixed(2) + ' 元'}}</span>
        <el-input class="input-money" v-model="actualityPay" placeholder="实收金额" type="number" min="0"></el-input>
      </div>
      <div class="pay-form">  
        <span>备注：</span>
        <el-input v-model="comment" placeholder="折扣,去零等" type="textarea" :rows="1"></el-input>
      </div> 
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitPay">确 定</el-button>
      </span>
    </el-dialog>


  </el-col>
</template>

<script>
  import Vue from 'vue'
  import ApiRequest from '../common/ApiRequest.js'
  import { Message, Loading, MessageBox} from 'element-ui'
  export default {
    data: function(){
      return {
        dialogVisible: false,
        currentOrder: {},
        actualityPay:'',
        comment: '',
        payType:'',
        pageSize: 20,
        currentPage: 1,
        totalItems: [],
        activeNames: [],
        inProductionStyle: {backgroundColor:'#20a0ff',color: 'white'},
        finishStyle: {color: '#fff', backgroundColor: '#13ce66', borderColor: '#13ce66'}
      }
    },
    mounted: function(){
      
      this.laodData();
      // trigger socket
      this.joinRoom();
    },
    computed:{
      displayItems: function(){
        return this.totalItems.slice((this.currentPage-1)*this.pageSize, this.currentPage*this.pageSize);
      },
      total: function(){
        return this.totalItems.length;
      }
    },
    sockets:{
      connect: function(){
        console.log('socket connected')
      },
      serverback: function(data){
        console.log('receive!!!');
        if(data==="newOrder"){
          this.laodData();
        }
      }
    },
    methods: {
      // add socket
      joinRoom: function(){
        this.$socket.emit("enter room", { uid: this.$parent.$parent.current_user.id });
      },
      laodData: function(){
        let url = "order/get_all_orders";
        let loadingInstance = Loading.service({text:'加载中......'});
        let self = this;
        ApiRequest.ajGet(url, (json)=>{
          if(json.success){
            self.totalItems = json.data;
            loadingInstance.close();
          }
          else{
            loadingInstance.close();
            Message.error(json.message);
          }
        })
      },
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
        let self = this;
        
        MessageBox.confirm('此操作将永久删除该订单, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          let loadingInstance = Loading.service({text:'加载中......'});
          ApiRequest.ajPost(url, data, (json)=>{
            if(json.success){
              let index = self.totalItems.indexOf(order);
              self.totalItems.splice(index,1);
              loadingInstance.close();
            }
            else{
              loadingInstance.close();
              Message.error(json.message);
            }
          })   
        }).catch(() => {
        });    
      },
      payOrder:function(order){

        let item_status_list = order['item_status_list'];
        let isCompleted = item_status_list.map((item)=>{return item=='制作完成'}).reduce((pre,cur)=>{return pre&&cur});
        // if(!isCompleted){
        //   Message.info('还有未完成项，不能结算');
        //   return
        // }else{
        //   this.dialogVisible = true;
        //   this.currentOrder = order;
        // }
        if(!isCompleted){
          MessageBox.confirm('还有制作中菜品, 确认先结账?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(()=>{
            this.dialogVisible = true;
            this.currentOrder = order;
          })
        }
        else{
          this.dialogVisible = true;
          this.currentOrder = order;
        }
      },
      submitPay: function(){
        let payType = this.payType;
        let actualityPay = this.actualityPay;
        let comment = this.comment;
        if(['现金','支付宝','微信','刷卡'].indexOf(payType) == -1){
          Message.error('请选择支付方式！');
          return
        }
        if(isNaN(actualityPay) || actualityPay=='' || actualityPay<0){
          Message.error('请选输入实付金额！');
          return 
        }
        let self = this;
        let data = {oid: this.currentOrder['oid'], payType: payType, actualityPay: actualityPay, comment: comment}
        let loadingInstance = Loading.service({text:'加载中......'});
        ApiRequest.ajPost('order/pay_order', data, (json)=>{
          if(json.success){
            let index = self.totalItems.indexOf(self.currentOrder);
            self.totalItems.splice(index,1);
            loadingInstance.close();
            self.dialogVisible = false;
          }
          else{
            loadingInstance.close();
            Message.error(json.message);
          }
        })
      },
      handleCurrentChange: function(currentPage){
        this.currentPage = parseInt(currentPage);
        this.displayItems = this.totalItems.slice((parseInt(currentPage)-1)*this.pageSize, parseInt(currentPage)*this.pageSize);
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
  .pay-form{
    margin-top: 1rem;
  }

</style>