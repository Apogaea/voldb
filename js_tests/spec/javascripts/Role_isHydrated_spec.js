describe("Role.isHydrated", function() {
  it("should not hydrated if it isNew", function() {
    var role = new app.Role();
    expect(role.isNew()).toBe(true);
    expect(role.isHydrated()).toBe(false);
  });

  it("should not hydrated if only has an id", function() {
    var role = new app.Role({id: 3});
    expect(role.isHydrated()).toBe(false);
  });

  it("should not hydrated if id and shifts", function() {
    var role = new app.Role({id: 3, shifts: []});
    expect(role.isHydrated()).toBe(false);
  });

  it("should not hydrated if it has any attribute other than an id", function() {
    var role = new app.Role({id: 3, shifts: [], other: "test"});
    expect(role.isHydrated()).toBe(true);
  });
});


