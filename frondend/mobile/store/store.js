import Vue from 'vue'
import Vuex from 'vuex'
import ApiRequest from '../../app/common/ApiRequest.js'

Vue.use(Vuex)

const state = {
    menuList:[],
    dataSource:[],
    table:{},
    selectedItemList:[],
    selectedItemQuantity:[],
    totalSelect:0,
    totalPrice:0.00,
    showTag:'index'
};

const mutations ={
    ADD_OF_ITEM(state,dateItem){
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
    REDUCE_OF_ITEM(state,dateItem){
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
    INIT_DATA(state,data){
        state.menuList = data.category;
        state.dataSource = data;
        state.table = data.table;
    },
    CHANGE_TAG(state,tag){
        
        state.showTag = tag;
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
                
                commit('INIT_DATA',data);
            }else{
                alert(json.message);
            }
        })
    },
    addItem({commit},dateItem){
        commit('ADD_OF_ITEM',dateItem);
    },

    reduceItem({commit},dateItem){
        commit('REDUCE_OF_ITEM',dateItem);
    },
    changeTag({commit},tag){
        commit('CHANGE_TAG',tag);
    }
}
export default new Vuex.Store({
    state,
    mutations,
    actions
})