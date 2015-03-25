describe("Shift.hasErrors", function() {
  it("should not have errors if unpopulated", function() {
    var shift = new app.Shift();
    expect(shift.hasErrors()).toBe(false);
  });

  it("should not have errors if empty array", function() {
    var shift = new app.Shift({claimErrors: []});
    expect(shift.hasErrors()).toBe(false);
  });

  it("should have errors if non-empty array", function() {
    var shift = new app.Shift({claimErrors: ["Some error"]});
    expect(shift.hasErrors()).toBe(true);
  });
});
