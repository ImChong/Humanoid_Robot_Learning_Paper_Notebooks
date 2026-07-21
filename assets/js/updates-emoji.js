/**
 * Seasonal / holiday emoji for the Update Log entry points.
 *
 * Replaces every `.js-updates-emoji` node with an emoji chosen from the
 * viewer's local calendar date (specific MM-DD first, then month fallback).
 * Default remains 📅 when nothing matches.
 */
(function (global) {
  'use strict';

  var DEFAULT_EMOJI = '📅';

  // Fixed solar-calendar days (MM-DD). Checked before month rules.
  var DAY_EMOJI = {
    '01-01': '🎊', // New Year
    '02-14': '💝', // Valentine's Day
    '03-08': '🌸', // International Women's Day
    '04-01': '🃏', // April Fools'
    '05-01': '🛠️', // Labor Day
    '06-01': '🎈', // Children's Day
    '10-01': '🎉', // National Day / early autumn festivity
    '10-31': '🎃', // Halloween
    '12-24': '🎄', // Christmas Eve
    '12-25': '🎄', // Christmas
    '12-31': '🎆'  // New Year's Eve
  };

  // Month fallbacks (1–12) when no specific day rule applies.
  var MONTH_EMOJI = {
    1: '❄️',
    2: '🧧', // Spring Festival season
    3: '🌱',
    4: '🌸',
    5: '🌿',
    6: '☀️',
    7: '🌊',
    8: '🍉',
    9: '🍂',
    10: '🍁',
    11: '🍁',
    12: '🎄'
  };

  function pad2(n) {
    return n < 10 ? '0' + n : String(n);
  }

  /**
   * @param {Date=} date Local date to resolve; defaults to now.
   * @returns {string} Emoji for that calendar day.
   */
  function coerceDate(date) {
    // Prefer duck-typing over `instanceof Date` so Node vm / iframe realms work.
    if (date && typeof date.getMonth === 'function' && typeof date.getDate === 'function'
        && typeof date.getTime === 'function' && !isNaN(date.getTime())) {
      return date;
    }
    return new Date();
  }

  function getUpdatesEmoji(date) {
    var d = coerceDate(date);
    var key = pad2(d.getMonth() + 1) + '-' + pad2(d.getDate());
    if (Object.prototype.hasOwnProperty.call(DAY_EMOJI, key)) {
      return DAY_EMOJI[key];
    }
    var monthEmoji = MONTH_EMOJI[d.getMonth() + 1];
    return monthEmoji || DEFAULT_EMOJI;
  }

  function applyUpdatesEmoji(date) {
    var emoji = getUpdatesEmoji(date);
    var nodes = document.querySelectorAll('.js-updates-emoji');
    for (var i = 0; i < nodes.length; i++) {
      if (nodes[i].textContent !== emoji) {
        nodes[i].textContent = emoji;
      }
    }
    return emoji;
  }

  global.getUpdatesEmoji = getUpdatesEmoji;
  global.applyUpdatesEmoji = applyUpdatesEmoji;

  // Expose tables for tests (read-only intent; do not mutate at runtime).
  global.__UPDATES_EMOJI_DAY__ = DAY_EMOJI;
  global.__UPDATES_EMOJI_MONTH__ = MONTH_EMOJI;
  global.__UPDATES_EMOJI_DEFAULT__ = DEFAULT_EMOJI;

  function boot() {
    applyUpdatesEmoji();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})(typeof window !== 'undefined' ? window : this);
