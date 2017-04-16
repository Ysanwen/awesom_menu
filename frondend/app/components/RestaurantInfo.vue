<template>  
  <el-col :span="20" class="left-nav-col">
    <div class="content">
      <div class="uploadArea">
        <label style="width: 80px" class="picture-label">展示图片</label>
        <div v-for="(item,index) in url_list" class="img-wrapper">
          <i class="el-icon-close" @click="handleRemovePicture(index)"></i>
          <img :src="createLink(item)" class="upload-label"/>
        </div>
        <label @click="handleSelectPicture" class="upload-label">
          <i class="el-icon-plus"></i>
        </label>
        <input type="file" @change="handleChange" name="upload" class="upload-button" ref="input"/>
      </div>
      <br/>
      <el-form label-width="80px" :model="info" ref="info">
        <el-form-item label="餐厅名称" prop="username">
          <el-input v-model="info.username"></el-input>
        </el-form-item>
        <el-form-item label="广告词" prop="type">
          <el-input v-model="info.ad" placeholder="用一句话描述餐厅特色"></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm">提交</el-button>
          <el-button  @click="cancel">取消</el-button>
        </el-form-item>
      </el-form>
    </div>
  </el-col>
</template>

<script>
  import ApiRequest from '../common/ApiRequest.js'
  import { Message } from 'element-ui'
  export default {
    name: 'restuarantInfo',
    data: function(){
      return {
        url_list: [],
        url_list_len: 0,
        upload_file_list:[],
        info: {
          username: '',
          ad: ''
        }
      }
    },
    created: function(){
      let self = this;
      ApiRequest.ajGet('user/get_current_user',(json)=>{
        if(json.success){
          let current_user = json.data;
          self.url_list = current_user.url_list;
          self.url_list_len = current_user.url_list.length;
          self.info.username = current_user.username;
          self.info.ad = current_user.ad;
        }else{
          Message.error(json.message)
        }
      })
    },
    methods: {
      handleSelectPicture:function () {
        this.$refs['input'].click()
      },
      handleRemovePicture:function(index){
        let remove_item = this.url_list[index];
        if(remove_item.indexOf('data') === -1){
          this.url_list.splice(index,1);
          this.url_list_len -= 1;
        }
        else{
          this.url_list.splice(index,1);
          this.upload_file_list.splice(index-this.url_list_len, 1);
        }
      },
      createLink:function(link){
        let url;
        if(link.indexOf('data') === -1){
          url = '/static/upload/' + link; 
        }
        else{
          url = link;
        }
        return url
      },
      handleChange:function () {
        let that = this;
        if(this.$refs['input'].files.length == 1){
          let picture_file = this.$refs['input'].files[0];
          let pattern = new RegExp('^image\/\\w+','i');
          if (!pattern.test(picture_file.type)){
            return false
          }
          let reader = new FileReader();
          reader.readAsDataURL(picture_file);
          reader.onload = function (e) {
            let read_result = this.result;// or e.target.result
            that.url_list.push(read_result);
          };

          that.upload_file_list.push(picture_file);
        }else {
          Message.alert('no picture selected');
        }
      },
      submitForm: function(){
        let self = this;
        let data = this.info;
        let url_list = this.url_list;
        data['url_list'] = [];
        for(let url of url_list){
          if(url.indexOf('data') === -1){
            data['url_list'].push(url)
          }
        }        
        let files = this.upload_file_list
        // change url_list to string
        data['url_list'] = JSON.stringify(data['url_list'])
        ApiRequest.ajUploadFile('user/create_info',{data:data,files:files},(json)=>{
          if(json.success){
            Message.success('创建成功！');
          }
        })
      },
      cancel: function(){
        this.$router.go(-1)
      }
    }
  }
</script>
<style scoped>
  .content{
    width: 50%;
    margin-left: 5%;
    /*margin-top: 50px;*/
  }
  .upload-button{
    display: none;
  }
  .picture-label{
    text-align: right;
    vertical-align: middle;
    float: left;
    font-size: 14px;
    color: #48576a;
    padding: 11px 12px 11px 0;
    box-sizing: border-box;
    width: 80px;
    height: 148px;
    line-height: 148px;
  }
  .img-wrapper{
    display: inline-block;
  }
  .el-icon-close{
    display: inline-block;
    position: absolute;
    color: white;
    font-size: 16px;
    border-radius: 6px;
    background-color: #13cd66;  
  }

  .upload-label{
    background-color: #fbfdff;
    border: 1px dashed #c0ccda;
    border-radius: 6px;
    box-sizing: border-box;
    width: 148px;
    height: 148px;
    cursor: pointer;
    line-height: 146px;
    vertical-align: top;
    display: inline-block;
    text-align: center;
    margin: auto;
  }
  .el-icon-plus{
    font-size: 28px;
    color: #8c939d;
  }
</style>