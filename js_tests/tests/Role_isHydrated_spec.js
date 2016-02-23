describe("Role.isHydrated", function() {
  it("should not hydrated if it isNew", function() {
    var role = new app.Role();
    chai.expect(role.isNew()).to.be.true;
    chai.expect(role.isHydrated()).to.be.false;
  });

  it("should not hydrated if only has an id", function() {
    var role = new app.Role({id: 3});
    chai.expect(role.isHydrated()).to.be.false;
  });

  it("should not hydrated if id and shifts", function() {
    var role = new app.Role({id: 3, shifts: []});
    chai.expect(role.isHydrated()).to.be.false;
  });

  it("should not hydrated if it has any attribute other than an id", function() {
    var role = new app.Role({id: 3, shifts: [], other: "test"});
    chai.expect(role.isHydrated()).to.be.true;
  });
});
