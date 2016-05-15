app.controller('DashboardCtrl',['$scope','$http','uiLoad','JQ_CONFIG',
	function($scope,$http,uiLoad,JQ_CONFIG){



		$scope.loadData=function(){
			$http.get("api/users/overview/").then(
				function(response){
					console.info(response.data);
					$scope.data=response.data;
					// var date=$scope.data.containers.date;
					$scope.drawDateContainer($scope.data.containers.date);
					$scope.drawPie($scope.data.containers.pie);
					// console.info($scope.getString($scope.options));
				},function(x){
					console.info(x);
				}
			)
		}
		$scope.title="控制面板";
		$scope.data={containers:{date:[]}};

		$scope.d = [[1,6.5],[2,6.5],[3,7],[4,8],[5,7.5],[6,7],[7,6.8],[8,7],[9,7.2],[10,7],[11,6.8],[12,7]];

		
		$scope.drawDateContainer=function(data){			
			$scope.dateContainers[0][0].data=data;

			$.plot("#createChart", $scope.dateContainers[0], $scope.dateContainers[1]);			
		}

		$scope.drawPie=function(data){
			var array=new Array(data.length);
			var i =0;
			for(var key in data){
				console.info(key);
				array[i]={label:key,data:data[key]};
				i++;
			}
			$scope.pie[0]=array;
			console.info(array);
			$.plot("#pieChart",$scope.pie[0],$scope.pie[1]);
		}

		$scope.dateContainers=[
			[{ 
				data: [],
				points: { show: true, radius: 6}, 
				lines: {show: true, tension:1, lineWidth: 5, fill: 0}
			}], 
			{
				colors: [$scope.app.color.primary],
				series: { shadowSize: 3 },
				xaxis:{ 
					font: { 
						color: '#ccc' 
					},
					position: 'bottom',
					// ticks: ["2016-5-12","2016-5-13"],
					mode: "time",
	    			timeformat: "%m/%d",
	    // 			timezone:"browser"
					
				},
				yaxis:{
					font: { color: '#ccc' },
					min: 0
				},
				grid: { hoverable: true, clickable: true, borderWidth: 0, color: '#ccc' },
				tooltip: true,
				tooltipOpts: { 
					content: 'create %y on %x',  
					defaultTheme: false, 
					shifts: { x: 0, y: 20 }
				}
			}
			];
		$scope.pie=[
			[],
			{
                series: { pie: { show: true, innerRadius: 0.5, stroke: { width: 0 }, label: { show: true, threshold: 0.05 } } },
                colors: [$scope.app.color.success,$scope.app.color.info,$scope.app.color.warning,$scope.app.color.danger],
                grid: { hoverable: true, clickable: true, borderWidth: 0, color: '#ccc' },   
                tooltip: true,
                tooltipOpts: { content: '%s: %p.0%' }
              }

		]

		uiLoad.load(JQ_CONFIG["plot"]).then(function(){
			$scope.loadData();
		});
		
}]);