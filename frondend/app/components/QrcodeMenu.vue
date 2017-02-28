<template>
  <el-col :span="20">
    <div class="create-qrcode">
      <el-input v-model="inputNumber" placeholder="请输入生成二维码数量" class="input-number"></el-input>
      <el-button type="primary" class="create-qrcode-button" @click="createQrcode">确定生成</el-button>
    </div>
    <el-card class="card-content" :body-style="{ padding: '0px' }" v-for="item in menuData">
      <img :src="'/static/upload/'+item['url_address'][0]" class="image">
      <div class="content-text">
          <el-input v-model="inputName" placeholder="请输入内容" class="input-name"></el-input>
          <el-button type="primary">修改</el-button>
      </div>
    </el-card>
  </el-col>
</template>

<script>
    import Vue from 'vue'
    import { Card,Message,Loading,Input,Button} from 'element-ui'
    import ApiRequest from '../common/ApiRequest.js'

    Vue.use(Card);
    Vue.use(Input);
    Vue.use(Button);
    
    export default {
      data:function() {
        return {
          menuData:[],
          inputNumber:"",
          inputName:""
        }
      },
      created:function(){
        let that = this;
        let loadingInstance = Loading.service({text:'加载中......'});
        ApiRequest.ajGet('menu/get_all_menus',(json)=>{
            if(json.success){
                that.menuData = json.data;
                loadingInstance.close();
            }else{
                loadingInstance.close();
                Message.error(json.message);
            }
        })
      },
      methods:{
        createQrcode:function(){
          let create_num = this.inputNumber;
          console.log(create_num);
          // TODO: add created qrcode function
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


.content-text {
  height: 3rem; 
  padding: 10px;
}
.input-name{
  width: 7rem;
}
.image {
  width: 12.5rem;
  height: 12.5rem;
  display: block;
}

</style>