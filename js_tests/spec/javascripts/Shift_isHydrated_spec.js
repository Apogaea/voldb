describe("Shift.isClaimable", function() {
  it("should not hydrated if it isNew", function() {
    var shift = new app.Shift();
    expect(shift.isNew()).toBe(true);
    expect(shift.isHydrated()).toBe(false);
  });

  it("should not hydrated if only has an id", function() {
    var shift = new app.Shift({id: 3});
    expect(shift.isHydrated()).toBe(false);
  });

  it("should not hydrated if it has any attribute other than an id", function() {
    var shift = new app.Shift({id: 3, other: "test"});
    expect(shift.isHydrated()).toBe(true);
  });
});


