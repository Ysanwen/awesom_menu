<template>  
  <el-col :span="4" class="left-nav-col">
    <el-menu default-active="1-1" class="el-menu-vertical-demo" @open="handleOpen" @close="handleClose" :router="useRouter">
      <el-submenu index="1">
        <template slot="title"><i class="el-icon-menu"></i>菜单管理</template>
          <el-menu-item index="1-1" :route='allMenu'>全部菜单</el-menu-item>
          <el-menu-item index="1-2" :route='addMenu'>新增菜单</el-menu-item>
          <el-menu-item index="1-3" :route='qrcodeMenu'>二维码菜单</el-menu-item>
      </el-submenu>
      <el-submenu index="2">
        <template slot="title"><i class="el-icon-menu"></i>订单管理</template>
          <el-menu-item index="2-1">进行中订单</el-menu-item>
          <el-menu-item index="2-2">已完成订单</el-menu-item>
      </el-submenu>
      <el-submenu index="3">
        <template slot="title"><i class="el-icon-menu"></i>其他</template>
          <el-menu-item index="3-1">其他一</el-menu-item>
          <el-menu-item index="3-2">其他二</el-menu-item>
      </el-submenu>
    </el-menu>
  </el-col>
</template>

<script>
   export default {
    data:function () {
      return{
        useRouter:true,
        allMenu:{path:'/allMenu'},
        addMenu:{path:'/addMenu'},
        qrcodeMenu:{path:'/qrcodeMenu'}
      }
    },
    methods: {
      handleOpen(key, keyPath) {
        console.log(key, keyPath);
      },
      handleClose(key, keyPath) {
        console.log(key, keyPath);
      }
    }
  }
</script>

<style scoped>
  .left-nav-col{
    height:100%;
    background-color: #eef1f6;
  }
</style>