app.controller('NavCtrl',['$scope',function($scope){

	$scope.navs=[
		// {
		// 	name: "Dashboard",
		// 	translate: "aside.nav.DASHBOARD",
		// 	icon: "glyphicon-stats text-primary-dker",
		// 	sub_menus: [
		// 		{
		// 			name: "Dashboard",
		// 			sref: "app.dashboard",
		// 			translate: "aside.nav.DASHBOARD"
		// 		}
		// 	]
		// },
		{
			name: "Dashboard",
			translate: "aside.nav.DASHBOARD",
			icon: "glyphicon-dashboard text-primary-dker",
			sref: "app.dashboard"

		},
		{
			name: "Applications",
			translate: "aside.nav.APPLICATIONS",
			icon: " glyphicon-th-large text-warning-dker",
			include:"app.applications",
			sub_menus: [
				{
					name: "应用列表",
					sref: "app.applications.list",
					translate:""
				}
			]
		},
		{
			name: "Images",
			translate: "aside.nav.IMAGES",
			icon: "glyphicon-briefcase text-success-dker",
			sref: "app.images"

		},
		{
			name: "Settings",
			translate: "aside.nav.SETTINGS",
			icon: "glyphicon-cog text-info-dker",
			sref: "app.settings"

		}
	]
}]);