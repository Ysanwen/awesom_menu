import Vue from 'vue'
import Vuex from 'vuex'
import ApiRequest from '../../app/common/ApiRequest.js'

Vue.use(Vuex)

const state = {
  userId: '',
  menuList:[],
  dataSource:[],
  table: {},
  selectedItemList: [],
  selectedItemQuantity: [],
  totalSelect: 0,
  totalPrice: 0.00,
  showTag: 'index',
  showOrder: false,
  orderItemList: [],
  orderItemQuantity: []
};

const mutations ={
  ADD_OF_ITEM(state, dateItem){
    // 已经被点完
    if(dateItem.quantity == 0){
      return
    }
    else{
      let type = dateItem.type;
      let data_source_list = state.dataSource[type]
      for(let item of data_source_list){
        if(item.id === dateItem.id){
          item.quantity = dateItem.quantity - 1;
        }
      }
      state.dataSource[type] = data_source_list
    }
    let item_index = state.selectedItemList.indexOf(dateItem);
    if(item_index<0){
      state.selectedItemList.push(dateItem);
      state.selectedItemQuantity.push(1);
    }else{
      state.selectedItemQuantity[item_index] +=1;
    }
    state.totalSelect += 1;
    state.totalPrice += dateItem['price']; 
  },
  REDUCE_OF_ITEM(state, dateItem){
    // 设置总数
    let type = dateItem.type;
    let data_source_list = state.dataSource[type]
    for(let item of data_source_list){
      if(item.id === dateItem.id){
        item.quantity = dateItem.quantity + 1;
      }
    }
    state.dataSource[type] = data_source_list
    // 跟新各选项数量
    let item_index = state.selectedItemList.indexOf(dateItem);
    if(state.selectedItemQuantity[item_index]==1){
      state.selectedItemQuantity.splice(item_index,1);
      state.selectedItemList.splice(item_index,1);
    }else{
      state.selectedItemQuantity[item_index] -=1;
    }
    state.totalSelect -= 1;
    state.totalPrice -= dateItem['price']
  },
  INIT_DATA(state, data){
    state.menuList = data.category;
    state.dataSource = data;
    state.table = data.table;
    state.orderItemList = data.order_info.menu_list;
    state.orderItemQuantity = data.order_info.quantity_list;
  },
  SET_USER_ID(state, uid){
    state.userId = uid;
  },
  CHANGE_TAG(state, tag){
    state.showTag = tag;
  },
  Move_SELECTED_TO_ORDER(state){
    state.orderItemList = state.orderItemList.concat(state.selectedItemList);
    state.orderItemQuantity = state.orderItemQuantity.concat(state.selectedItemQuantity)
    state.selectedItemList = [];
    state.selectedItemQuantity = [];
    state.totalSelect = 0;
    state.totalPrice = 0.00;
  },
  CHANGE_SHOW_ORDER(state, status){
    state.showOrder = status;
  }
};

const actions = {
  initData({commit}){
    let getQueryVariable = function(variable){
      var query = window.location.search.substring(1);
      var vars = query.split("&");
      for (var i=0;i<vars.length;i++) {
       var pair = vars[i].split("=");
       if(pair[0] == variable){return pair[1];}
      }
      return(false);
    }
    let url_par = getQueryVariable('uid');
    let table_id = getQueryVariable('table_id');
    ApiRequest.ajGet('category/get_categories_menu?uid='+url_par+'&table_id='+table_id,(json)=>{
      if(json.success){
        let data = json.data;
        
        commit('INIT_DATA', data);
        commit('SET_USER_ID', url_par);
      }else{
        alert(json.message);
      }
    })
  },
  addItem({commit}, dateItem){
    commit('ADD_OF_ITEM', dateItem);
  },

  reduceItem({commit}, dateItem){
    commit('REDUCE_OF_ITEM', dateItem);
  },
  changeTag({commit}, tag){
    commit('CHANGE_TAG', tag);
  },
  moveSelectedToOrder({commit}){
    commit('Move_SELECTED_TO_ORDER')
  },
  changeShowOrder({commit},status){
    commit('CHANGE_SHOW_ORDER',status);
  }
}
export default new Vuex.Store({
  state,
  mutations,
  actions
})