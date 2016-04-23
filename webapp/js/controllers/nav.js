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
			icon: "glyphicon-stats text-primary-dker",
			sref: "app.dashboard"

		},
		{
			name: "Applications",
			translate: "aside.nav.APPLICATIONS",
			icon: " glyphicon-th-large text-warning-dker",
			sref: "app.applications"
		},
		{
			name: "Settings",
			translate: "aside.nav.SETTINGS",
			icon: "glyphicon-cog text-info-dker",
			sref: "app.settings"

		}
	]
}]);