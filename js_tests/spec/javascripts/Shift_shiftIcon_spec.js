describe("Shift.shiftIcon", function() {
  it("should have the locked icon", function() {
    var shift = new app.Shift({is_locked: true, open_slot_count: false});
    expect(shift.shiftIcon()).toEqual("lock");
  });

  it("should have the locked icon even if has open slots", function() {
    var shift = new app.Shift({is_locked: true, open_slot_count: true});
    expect(shift.shiftIcon()).toEqual("lock");
  });

  it("should have the plus icon if has open slots", function() {
    var shift = new app.Shift({is_locked: false, open_slot_count: true});
    expect(shift.shiftIcon()).toEqual("plus-sign");
  });

  it("should have the minus icon if does not have open slots", function() {
    var shift = new app.Shift({is_locked: false, open_slot_count: false});
    expect(shift.shiftIcon()).toEqual("minus-sign");
  });
});
