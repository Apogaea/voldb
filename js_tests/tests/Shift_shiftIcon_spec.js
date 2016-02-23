describe("Shift.shiftIcon", function() {
  it("should have the locked icon", function() {
    var shift = new app.Shift({is_locked: true, open_slot_count: false});
    chai.expect(shift.shiftIcon()).to.equal("lock");
  });

  it("should have the locked icon even if has open slots", function() {
    var shift = new app.Shift({is_locked: true, open_slot_count: true});
    chai.expect(shift.shiftIcon()).to.equal("lock");
  });

  it("should have the plus icon if has open slots", function() {
    var shift = new app.Shift({is_locked: false, open_slot_count: true});
    chai.expect(shift.shiftIcon()).to.equal("plus-sign");
  });

  it("should have the minus icon if does not have open slots", function() {
    var shift = new app.Shift({is_locked: false, open_slot_count: false});
    chai.expect(shift.shiftIcon()).to.equal("minus-sign");
  });
});
