

(define (problem BW-rand-6)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 )
(:init
(arm-empty)
(on b1 b4)
(on-table b2)
(on b3 b1)
(on-table b4)
(on-table b5)
(on b6 b2)
(clear b3)
(clear b5)
(clear b6)
)
(:goal
(and
(on b2 b1)
(on b5 b6))
)
)


