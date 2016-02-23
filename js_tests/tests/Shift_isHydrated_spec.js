describe("Shift.isHydrated", function() {
  it("should not hydrated if it isNew", function() {
    var shift = new app.Shift();
    chai.expect(shift.isNew()).to.be.true;
    chai.expect(shift.isHydrated()).to.be.false;
  });

  it("should not hydrated if only has an id", function() {
    var shift = new app.Shift({id: 3});
    chai.expect(shift.isHydrated()).to.be.false;
  });

  it("should not hydrated if only id and slots", function() {
    var shift = new app.Shift({id: 3, claimed_slots: []});
    chai.expect(shift.isHydrated()).to.be.false;
  });

  it("should not hydrated if it has any attribute other than an id", function() {
    var shift = new app.Shift({id: 3, claimed_slots: [], other: "test"});
    chai.expect(shift.isHydrated()).to.be.true;
  });
});
