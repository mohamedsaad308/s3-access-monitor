import MainNavigation from "./MainNavigation";

function Layout(props) {
  return (
    <div>
      <main className="container">
        <MainNavigation />
        {props.children}
      </main>
    </div>
  );
}

export default Layout;
