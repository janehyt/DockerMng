'use strict';

/* Filters */
// need load the moment.js to use this filter. 
angular.module('app')
  .filter('fromNow', function() {
    return function(date) {
    	
    		return moment(date).fromNow();
      
    }
  });

 app.filter('size',function(){
 	return function(size){
 		if(!size)
 			return "0.00 B"
 		if(size<1024)
 			return size.toFixed(2)+" B";
 		if(size<1048576)
 			return (size/1024).toFixed(2)+" KB";

 		return (size/1048576).toFixed(2)+" MB";
 	}
 }).filter('time',function(){
 	return function(data){
 		if(!data){
 			return ""
 		}
 		var date = new Date(data);
 		var now = new Date();
 		var second = Math.round((now-date)/1000);
 		if(second<10)
 			return "刚刚";
 		if(second<60)
 			return second+"秒前";
 		if(second<3600)
 			return Math.round(second/60)+"分钟前";
 		if(second<86400)
 			return Math.round(second/3600)+"小时前";
 		if(second<604800)
 			return Math.round(second/86400)+"天前";
 		var month=date.getMonth()+1;
 		var day = date.getDate();
 		if(month<10)
 			month = '0'+month;
 		if(day<10)
 			day='0'+day
 		return date.getFullYear()+"-"+month+"-"+day;
 	}
 }).filter('largeNumber',function(){
 	return function(data){
 		var rule = [
			{name:'10M+',min:"10000000"},
			{name:'5M+',min:"5000000"},
			{name:'1M+',min:"1000000"},
			{name:'500K+',min:"500000"},
			{name:'100K+',min:"100000"},
			{name:'50K+',min:"50000"},
			{name:'10K+',min:"10000"}];
		for(var i =0;i<rule.length; i++){
			if(data>rule[i].min){
				return rule[i].name;
			}
		}
		if(data>1000)
			return (data/1000).toFixed(1)+"K";
		return data;
 	}
 }).filter('filterOfficial',function(){
 	return function(namespace){
 		if(namespace=='library')
 			return '';
 		return namespace+"/";
 	}
 })