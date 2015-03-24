describe("Shift.cliamUrl", function() {
  it("should be the right url", function() {
    var shift = new app.Shift({id: 3});
    expect(shift.cliamUrl().toEqual("/v2/shifts/3/claim/");
  });
});
