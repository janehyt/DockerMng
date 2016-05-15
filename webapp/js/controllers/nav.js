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
			icon: "glyphicon-th-large text-warning-dker",
			sref: "app.applications"
		},
		// {
		// 	name: "Applications",
		// 	translate: "aside.nav.APPLICATIONS",
		// 	icon: " glyphicon-th-large text-warning-dker",
		// 	include:"app.applications",
		// 	sub_menus: [
		// 		{
		// 			name: "应用列表",
		// 			sref: "app.applications.list",
		// 			translate:""
		// 		}
		// 	]
		// },
		{
			name: "Repo",
			translate: "aside.nav.REPO",
			icon: "glyphicon-briefcase text-success-dker",
			sref: "app.repos"

		},
		{
			name: "File",
			translate: "aside.nav.FILE",
			icon: "glyphicon-file text-danger-dker",
			sref: "app.file"
		},
		{
			name: "Reset Password",
			translate: "aside.nav.RESET",
			icon: "glyphicon-cog text-info-dker",
			sref: "app.reset"

		}
	]
}]);