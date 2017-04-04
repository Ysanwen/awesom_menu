<template>
  <el-col :span="20">
    <div class="create-qrcode no-print">
      <el-input v-model="inputNumber" placeholder="请输入生成二维码数量" class="input-number"></el-input>
      <el-button type="primary" class="create-qrcode-button" @click="createQrcode">确定生成</el-button>
    </div>
    <el-card class="card-content" :body-style="{ padding: '0px' }" v-for="(item,index) in qrcodeData">
      <img :src="'/static/qrcode/'+item['url_address']" class="image">
      <qrcode-modify :item_dict="item"></qrcode-modify>
    </el-card>
  </el-col>
</template>

<script>
    import Vue from 'vue'
    import { Card,Message,Loading,Input,Button} from 'element-ui'
    import QrcodeModify from './QrcodeModify.vue'
    import ApiRequest from '../common/ApiRequest.js'

    Vue.use(Card);
    Vue.use(Input);
    Vue.use(Button);
    
    export default {
      data:function() {
        return {
          qrcodeData:[],
          inputNumber:"",
          
        }
      },
      components:{
        QrcodeModify
      },
      created:function(){
        let that = this;
        let loadingInstance = Loading.service({text:'加载中......'});
        ApiRequest.ajGet('qrcode/get_all_qrcodes',(json)=>{
            if(json.success){
                that.qrcodeData = json.data;
                loadingInstance.close();
            }else{
                loadingInstance.close();
                Message.error({message:json.message,showClose:true});
            }
        })
      },
      methods:{
        createQrcode:function(){
          let that = this;
          let loadingInstance = Loading.service({text:'加载中......'});
          let create_num = parseInt(this.inputNumber);
          // TODO: add created qrcode function
          ApiRequest.ajGet('qrcode/create_qrcode?create_quantity='+create_num,(json)=>{
            if(json.success){
              that.qrcodeData = json.data;
              loadingInstance.close();
            }else{
              loadingInstance.close();
              Message.error({message:json.message,showClose:true});
            }
          })
        }
      }
    }
</script>

<style scoped>
.card-content {
    width: 12.5rem;
    height: 15.5rem;
    font-size: 14px;
    margin-left: 5px;
    margin-top: 5px;
    display: inline-block;
    border: 1px solid #d1dbe5;
    border-radius: 4px;
    background-color: #fff;
    overflow: hidden;
    box-shadow: 0 2px 4px 0 rgba(0, 0, 0, .12), 0 0 6px 0 rgba(0, 0, 0, .04)
}
.create-qrcode{
  margin-left: 1rem;
  margin-top: 1rem;
}
.input-number{
  display: inline-block;
  width: 12rem;
}
.create-qrcode-button{
  display: inline-block;
}
.image {
  width: 12.5rem;
  height: 12.5rem;
  display: block;
}

</style>