app.controller('DashboardCtrl',['$scope','uiLoad','JQ_CONFIG','User',
	function($scope,uiLoad,JQ_CONFIG,User){

		$scope.init=function(){
			$scope.title="控制面板";
			$scope.data={containers:{date:[]}};
			User.overview().then(
				function(data){
					$scope.data=data;
					$scope.drawDateContainer($scope.data.containers.date);
					$scope.drawPie($scope.data.containers.pie);
				},
				function(x){
					console.info(x)
				});
		}
		

		
		$scope.drawDateContainer=function(data){			
			$scope.dateContainers[0][0].data=data;

			$.plot("#createChart", $scope.dateContainers[0], $scope.dateContainers[1]);			
		}

		$scope.drawPie=function(data){
			var array=new Array(data.length);
			var i =0;
			for(var key in data){
				// console.info(key);
				array[i]={label:key,data:data[key]};
				i++;
			}
			$scope.pie[0]=array;
			// console.info(array);
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
			$scope.init();
		});
		
}]);