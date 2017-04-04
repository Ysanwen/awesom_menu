<template>
<div class="content-text">
  <div v-if="showInfo" class="show-info" :source="copyItemDict">
    <span class="table-num">当前桌号：{{ new_item_dict["table_name"] }}</span>
    <el-button type="primary" class="content-button no-print" @click="showEdit">修改</el-button>
    <el-button type="primary" class="content-button no-print" @click="print">打印</el-button>
  </div>
  <div v-else class="edit-form">
    <el-input v-model="inputName" placeholder="请输入桌号" class="input-name"></el-input>
    <el-button type="primary" class="edit-button" @click="submitRename(new_item_dict)">确定</el-button>
    <el-button type="primary" class="edit-button" @click="submitCancel">取消</el-button>
  </div>
</div>
</template>

<script>
import { Loading } from 'element-ui'
import ApiRequest from '../common/ApiRequest.js'

export default {
  data:function(){
    return {showInfo:true,inputName:'',new_item_dict:{}}
  },

  props:['item_dict'],

  computed:{
    copyItemDict:function(){
      for(let item in this.item_dict){
        this.new_item_dict[item] = this.item_dict[item]
      }
      return true
    }
  },

  methods:{
    showEdit:function () {
      this.showInfo = false
    },

    submitRename:function(item,data){
      let new_name = this.inputName.replace(/\s/g,"");
     
      if(new_name.length == 0){
        Message.error({message:'请输入桌号',showClose:true});
        this.inputName='';
        return false  
      }else{
        let loadingInstance = Loading.service({text:'更新中......'});
        let that = this;
        let id = parseInt(item['id']);
        let post_data = {id:id,table_name:new_name}
        ApiRequest.ajPost('qrcode/update_qrcode',post_data,(json)=>{
          if(json.success){
            that.new_item_dict['table_name'] = json.data['table_name'];
            loadingInstance.close();
            that.showInfo = true; 
          }else{
            loadingInstance.close();
            Message.error({message:json.message,showClose:true});
          }
        })
      }
      // this.showInfo = true;
    },
    print: function(){
      window.print();
    },
    submitCancel:function(){
      this.inputName = '';
      this.showInfo= true;
    }
  }
}
</script>

<style scoped>
.content-text {
  height: 3rem; 
  text-align: center;
}
.table-num{
  display: block;
  text-align: center;
}
.content-button{
  height: 1.5rem;
  padding: 0px;
  width: 3.5rem;
}
.edit-form{
  height: 3rem;
}

.input-name{
  width: 7rem;
  float: left;
  padding-left: 1rem;
  margin-top: 0.25rem;
}
.edit-button{
  height: 1.25rem;
  padding: 0px;
  margin-right: 0.5rem;
  width: 3rem;
  float: right;
  margin-bottom: 5px
}
</style>