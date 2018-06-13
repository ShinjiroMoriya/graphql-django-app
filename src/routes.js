import AppContainer from "./AppContainer";
import Top from "./Top";
import Profile from "./Profile";

const Routes = [
  {
    component: AppContainer,
    routes: [
      {
        path: "/",
        exact: true,
        component: Top
      },
      {
        path: "/profile",
        component: Profile
      }
    ]
  }
];

export default Routes;
